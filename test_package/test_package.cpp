#include <assimp/Importer.hpp>  // C++ importer interface
#include <assimp/postprocess.h> // Post processing flags
#include <assimp/scene.h>       // Output data structure
#include <iostream>

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "Must specify path to test mesh" << std::endl;
    return 1;
  }

  Assimp::Importer importer;

  // And have it read the given file with some example postprocessing
  // Usually - if speed is not the most important aspect for you - you'll
  // propably to request more postprocessing than we do in this example.
  const aiScene *scene = importer.ReadFile(
      argv[1], aiProcess_CalcTangentSpace | aiProcess_Triangulate |
                   aiProcess_JoinIdenticalVertices | aiProcess_SortByPType);

  if (!scene) {
    std::cerr << "Failed to open " << argv[1]
              << ". Reason: " << importer.GetErrorString() << std::endl;
    return 1;
  }

  std::cout << "Successfully loaded " << argv[1] << std::endl;

  return 0;
}
