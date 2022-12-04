
#include "mbed.h"
#include "wifi_helper.h"
#include <string>

// Sensors drivers present in the BSP library
#include "stm32l475e_iot01_gyro.h"
#include "stm32l475e_iot01_accelero.h"
#include "stm32l475e_iot01_tsensor.h"
#include "stm32l475e_iot01_hsensor.h"
#define IP_ADDRESS "" //YOUR_IP_ADDRESS
#define PORT 6533 //YOUR_PORT


class SocketDemo {
    static constexpr size_t MAX_NUMBER_OF_ACCESS_POINTS = 10;
    static constexpr size_t MAX_MESSAGE_RECEIVED_LENGTH = 100;


public:
    SocketDemo() : _net(NetworkInterface::get_default_instance())
    {
    }

    ~SocketDemo()
    {
        if (_net) {
            _net->disconnect();
        }
    }

    void run()
    {
        if (!_net) {
            printf("Error! No network interface found.\r\n");
            return;
        }

        /* if we're using a wifi interface run a quick scan */
        if (_net->wifiInterface()) {
            /* the scan is not required to connect and only serves to show visible access points */
            wifi_scan();
        }

        /* connect will perform the action appropriate to the interface type to connect to the network */

        printf("Connecting to the network...\r\n");

        nsapi_size_or_error_t result = _net->connect();
        if (result != 0) {
            printf("Error! _net->connect() returned: %d\r\n", result);
            return;
        }

        print_network_info();

        /* opening the socket only allocates resources */
        result = _socket.open(_net);
        if (result != 0) {
            printf("Error! _socket.open() returned: %d\r\n", result);
            return;
        }

        /* now we have to find where to connect */

        SocketAddress address;
        address.set_ip_address(IP_ADDRESS);
        address.set_port(PORT);

        /* we are connected to the network but since we're using a connection oriented
         * protocol we still need to open a connection on the socket */


        result = _socket.connect(address);
        if (result != 0) {
            printf("Error! _socket.connect() returned: %d\r\n", result);
            return;
        }

        /* exchange an HTTP request and response */
        //sensor part//
        float sensor_value = 0;
        int16_t pDataXYZ[3] = {0};
        float pGyroDataXYZ[3] = {0};
        int sample_num=0;
       
        BSP_GYRO_Init();
        BSP_ACCELERO_Init();
        BSP_TSENSOR_Init();
        //remove offset
        float avgx=0,avgy=0,avgz=0;
        float avggx=0,avggy=0,avggz=0;
        for(int i=0;i<20;i++){
            BSP_ACCELERO_AccGetXYZ(pDataXYZ);
            float x = pDataXYZ[0], y = pDataXYZ[1], z = pDataXYZ[2];
            avgx+=x;
            avgy+=y;
            avgz+=z;
            BSP_GYRO_GetXYZ(pGyroDataXYZ);
            float gx = pGyroDataXYZ[0], gy = pGyroDataXYZ[1], gz = pGyroDataXYZ[2];
            avggx+=gx;
            avggy+=gy;
            avggz+=gz;
        }
        avgx/=20;
        avgy/=20;
        avgz/=20;
        avggx/=20;
        avggy/=20;
        avggz/=20;
        // printf("avgx,y,z=%f,%f,%f",avgx,avgy,avgz);
        int cnt=0;
        int start=0;
        int last_state=-1; //-1 start 0 stopped 1 opening 2 closing

        while (1){
            // ++sample_num;
            BSP_ACCELERO_AccGetXYZ(pDataXYZ);
            float x = pDataXYZ[0], y = pDataXYZ[1], z = pDataXYZ[2];
            BSP_GYRO_GetXYZ(pGyroDataXYZ);
            float gx = pGyroDataXYZ[0], gy = pGyroDataXYZ[1], gz = pGyroDataXYZ[2];
            float temprature = BSP_TSENSOR_ReadTemp();
            float humidity=BSP_HSENSOR_ReadHumidity();
            char acc_json[1024];
            char message[1024];
            bool send=1;
            if((x-avgx)*(x-avgx)+(y-avgy)*(y-avgy)>=20){
                if(cnt==0){
                    start=y-avgy;
                }
                cnt++;
                if(cnt>=8){
                    if(start>0){
                        if(last_state==1){
                            send=0;
                        }
                        sprintf(message,"\"door opening\"");
                        last_state=1;
                    }
                    else{
                        if(last_state==2){
                            send=0;
                        }
                        sprintf(message,"\"door closing\"");
                        last_state=2;
                    }
                }
                else{
                    if(last_state==0){
                        send=0;
                    }
                    sprintf(message,"\"door stopped\"");
                    last_state=0;
                }
            }
            else{
                cnt=0;
                if(last_state==0){
                    send=0;
                }
                sprintf(message,"\"door stopped\"");
                last_state=0;
            }
            int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
            // int len = sprintf(acc_json,"{\"x\":%f,\"y\":%f,\"z\":%f,\"gx\":%f,\"gy\":%f,\"gz\":%f,\"s\":%d,\"m\":%s}",(float)((int)((x-avgx)*10000))/10000,(float)((int)((y-avgy)*10000))/10000, (float)((int)((z-avgz)*10000))/10000,gx-avggx,gy-avggy,gz-avggz,sample_num,message);
            if(send!=0){
                nsapi_size_or_error_t response = 0;
                response = _socket.send(acc_json,len);
                if (0 >= response){
                    printf("Error seding: %d\n", response);
                    _socket.close();
                    break;
                }
            }
            
            ThisThread::sleep_for(200ms);
        } 


        printf("Demo concluded successfully \r\n");
    }

private:

    void wifi_scan()
    {
        WiFiInterface *wifi = _net->wifiInterface();

        WiFiAccessPoint ap[MAX_NUMBER_OF_ACCESS_POINTS];

        /* scan call returns number of access points found */
        int result = wifi->scan(ap, MAX_NUMBER_OF_ACCESS_POINTS);

        if (result <= 0) {
            printf("WiFiInterface::scan() failed with return value: %d\r\n", result);
            return;
        }

        printf("%d networks available:\r\n", result);

        for (int i = 0; i < result; i++) {
            printf("Network: %s secured: %s BSSID: %hhX:%hhX:%hhX:%hhx:%hhx:%hhx RSSI: %hhd Ch: %hhd\r\n",
                   ap[i].get_ssid(), get_security_string(ap[i].get_security()),
                   ap[i].get_bssid()[0], ap[i].get_bssid()[1], ap[i].get_bssid()[2],
                   ap[i].get_bssid()[3], ap[i].get_bssid()[4], ap[i].get_bssid()[5],
                   ap[i].get_rssi(), ap[i].get_channel());
        }
        printf("\r\n");
    }

    void print_network_info()
    {
        /* print the network info */
        SocketAddress a;
        _net->get_ip_address(&a);
        printf("IP address: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
        _net->get_netmask(&a);
        printf("Netmask: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
        _net->get_gateway(&a);
        printf("Gateway: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
    }

private:
    NetworkInterface *_net;

#if MBED_CONF_APP_USE_TLS_SOCKET
    TLSSocket _socket;
#else
    TCPSocket _socket;
#endif // MBED_CONF_APP_USE_TLS_SOCKET
};

int main() {
    printf("\r\nStarting Final_Project\r\n\r\n");


    SocketDemo *example = new SocketDemo();
    MBED_ASSERT(example);
    example->run();
    printf("END");
    return 0;
}
