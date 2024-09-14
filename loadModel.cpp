#include <tensorflow/core/public/session.h>
#include <tensorflow/core/protobuf/meta_graph.pb.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <winsock2.h>

// Function to load the model
std::unique_ptr<tensorflow::Session> LoadModel(const std::string& model_path) {
    tensorflow::Session* session;
    tensorflow::Status status = tensorflow::NewSession(tensorflow::SessionOptions(), &session);
    if (!status.ok()) {
        throw std::runtime_error("Failed to create TensorFlow session: " + status.ToString());
    }

    tensorflow::MetaGraphDef graph_def;
    status = tensorflow::ReadBinaryProto(tensorflow::Env::Default(), model_path, &graph_def);
    if (!status.ok()) {
        throw std::runtime_error("Failed to load model: " + status.ToString());
    }

    status = session->Create(graph_def.graph_def());
    if (!status.ok()) {
        throw std::runtime_error("Failed to create graph: " + status.ToString());
    }

    return std::unique_ptr<tensorflow::Session>(session);
}

// Function to make predictions
std::vector<float> Predict(std::unique_ptr<tensorflow::Session>& session, const std::vector<float>& input_data) {
    tensorflow::Tensor input_tensor(tensorflow::DT_FLOAT, tensorflow::TensorShape({1, input_data.size()}));
    std::copy(input_data.begin(), input_data.end(), input_tensor.flat<float>().data());

    std::vector<tensorflow::Tensor> outputs;
    tensorflow::Status status = session->Run({{"serving_default_input_1:0", input_tensor}}, {"StatefulPartitionedCall:0"}, {}, &outputs);
    if (!status.ok()) {
        throw std::runtime_error("Failed to run model: " + status.ToString());
    }

    return std::vector<float>(outputs[0].flat<float>().data(), outputs[0].flat<float>().data() + outputs[0].NumElements());
}

// Function to save live data
void SaveLiveData(const std::vector<float>& data, const std::string& file_path) {
    std::ofstream file(file_path, std::ios::app);
    for (const auto& value : data) {
        file << value << ",";
    }
    file << std::endl;
    file.close();
}

int main() {
    // Load the model
    auto session = LoadModel("ppo_forex_trading_model_tf");

    // Initialize Winsock
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    // Create a socket
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    // Bind the socket
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(5555);
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));

    // Listen for incoming connections
    listen(serverSocket, SOMAXCONN);

    while (true) {
        // Accept a client socket
        SOCKET clientSocket = accept(serverSocket, NULL, NULL);

        // Receive data from the client
        char recvBuffer[1024];
        int bytesReceived = recv(clientSocket, recvBuffer, 1024, 0);
        if (bytesReceived > 0) {
            std::vector<float> input_data(reinterpret_cast<float*>(recvBuffer), reinterpret_cast<float*>(recvBuffer) + bytesReceived / sizeof(float));

            // Make predictions
            std::vector<float> predictions = Predict(session, input_data);

            // Send predictions back to the client
            send(clientSocket, reinterpret_cast<char*>(predictions.data()), predictions.size() * sizeof(float), 0);

            // Save live data for further training
            SaveLiveData(input_data, "live_data.csv");
        }

        // Close the client socket
        closesocket(clientSocket);
    }

    // Clean up
    closesocket(serverSocket);
    WSACleanup();

    return 0;
}