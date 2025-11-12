#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <filesystem>
#include <json/json.h>
// include a JSON library like jsoncpp
// (install via package manager or include the library manually)

namespace fs = std::filesystem;

// constants
const int SEQUENCE_LENGTH_DEFAULT = 20;
const int SEQUENCE_F0_DEFAULT = 0;
const int SEQUENCE_F1_DEFAULT = 1;
// const std::string OUTPUT_FOLDER = "./outputs/";  // use while running locally
const std::string OUTPUT_FOLDER = "/data/outputs/"; // use while running in docker

std::vector<int> generate_fibonacci(int length, int f0 = 0, int f1 = 1)
{
    // Generate Fibonacci sequence of given length starting with f0 and f1.
    std::vector<int> sequence{f0, f1};
    for (int i = 2; i < length; ++i)
    {
        sequence.push_back(sequence[i - 1] + sequence[i - 2]);
    }
    return sequence;
}

int get_env_var(const std::string &name, int default_value)
{
    // Retrieve environment variable and cast to the specified type.
    const char *env_val = std::getenv(name.c_str());
    if (env_val)
    {
        try
        {
            return std::stoi(env_val);
        }
        catch (const std::invalid_argument &)
        {
            std::cerr << "Error: " << name << " must be an integer" << std::endl;
            std::exit(EXIT_FAILURE);
        }
    }
    return default_value;
}

void save_to_file(const std::string &filepath, const std::vector<int> &sequence)
{
    // Save sequence to JSON file

    fs::create_directories(OUTPUT_FOLDER);

    Json::Value root;
    Json::StreamWriterBuilder writer;
    root["sequence"] = Json::arrayValue;

    for (int num : sequence)
    {
        root["sequence"].append(num);
    }

    std::ofstream file(filepath);
    if (file.is_open())
    {
        file << Json::writeString(writer, root);
        file.close();
        std::cout << "Sequence saved to " << filepath << std::endl;
    }
    else
    {
        std::cerr << "Error: Unable to open file " << filepath << std::endl;
    }
}

int main()
{
    std::cout << "Starting Fibonacci model." << std::endl;

    // retrieve input parameters from environment variables or use defaults
    int sequence_length = get_env_var("SEQUENCE_LENGTH", SEQUENCE_LENGTH_DEFAULT);
    int sequence_f0 = get_env_var("SEQUENCE_F0", SEQUENCE_F0_DEFAULT);
    int sequence_f1 = get_env_var("SEQUENCE_F1", SEQUENCE_F1_DEFAULT);

    // generate Fibonacci sequence
    std::vector<int> sequence = generate_fibonacci(sequence_length, sequence_f0, sequence_f1);

    // output results to file
    save_to_file(OUTPUT_FOLDER + "sequence.json", sequence);

    std::cout << "Finished Fibonacci model." << std::endl;

    return 0;
}
