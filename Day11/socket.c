#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 8080
#define MAX_BUFFER_SIZE 50000
void handle_request(int client_socket) {
    char request[MAX_BUFFER_SIZE];
    char response[MAX_BUFFER_SIZE];

    // 클라이언트로부터 요청 받기
    if (read(client_socket, request, sizeof(request)) < 0) {
        perror("Failed to read request");
        return;
    }

    // GET 요청 처리
    if (strstr(request, "GET") != NULL) {
        if (strstr(request, "game.jpg") != NULL) {
            // 이미지 파일 읽기
            FILE* image_file = fopen("game.jpg", "rb");
            if (!image_file) {
                perror("Failed to open image file");
                return;
            }

            // 이미지 파일 크기 확인
            fseek(image_file, 0, SEEK_END);
            long image_size = ftell(image_file);
            fseek(image_file, 0, SEEK_SET);

            // 이미지 파일을 메모리에 저장하기 위한 버퍼 동적 할당
            char* image_buffer = (char*)malloc(image_size);
            if (!image_buffer) {
                perror("Failed to allocate memory for image");
                fclose(image_file);
                return;
            }

            // 이미지 파일 읽기
            if (fread(image_buffer, 1, image_size, image_file) != image_size) {
                perror("Failed to read image file");
                fclose(image_file);
                free(image_buffer);
                return;
            }

            fclose(image_file);

            // 이미지 응답 전송
            sprintf(response, "HTTP/1.1 200 OK\r\n"
                              "Server: Linux Web Server\r\n"
                              "Content-Type: image/jpeg\r\n"
                              "Content-Length: %ld\r\n\r\n", image_size);

            // 응답 헤더 전송
            if (write(client_socket, response, strlen(response)) < 0) {
                perror("Failed to send response header");
                free(image_buffer);
                return;
            }

            // 이미지 데이터 전송
            if (write(client_socket, image_buffer, image_size) < 0) {
                perror("Failed to send image data");
                free(image_buffer);
                return;
            }

            free(image_buffer);
        } else {
            // 나머지 요청에 대한 응답
            sprintf(response, "HTTP/1.1 200 OK\r\n"
                              "Server: Linux Web Server\r\n"
                              "Content-Type: text/html; charset=UTF-8\r\n\r\n"
                              "<!DOCTYPE html>\r\n"
                              "<html><head><title>My Web Page</title>\r\n"
                              "<style>body {background-color: #FFFF00 }</style></head>\r\n"
                              "<body><center><h1>Hello world!!</h1><br>\r\n"
                              "<img src=\"game.jpg\"></center></body></html>\r\n");

            // 클라이언트에 응답 전송
            if (write(client_socket, response, strlen(response)) < 0) {
                perror("Failed to send response");
                return;
            }
        }
    }

    close(client_socket);
}

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_size;

    // 소켓 생성
    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Failed to create socket");
        return 1;
    }

    // 서버 주소 설정
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);

    // 소켓에 주소 할당
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        perror("Failed to bind socket");
        return 1;
    }

    // 연결 대기 상태로 진입
    if (listen(server_socket, 5) < 0) {
        perror("Failed to listen");
        return 1;
    }

    printf("Web server is running on port %d\n", PORT);

    while (1) {
        client_address_size = sizeof(client_address);

        // 클라이언트의 연결 요청 수락
        if ((client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_size)) < 0) {
            perror("Failed to accept connection");
            return 1;
        }

        printf("Client connected: %s:%d\n", inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port));

        // 클라이언트 요청 처리
        handle_request(client_socket);
    }

    // 소켓 닫기
    close(server_socket);

    return 0;
}
