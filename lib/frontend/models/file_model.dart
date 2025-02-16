import 'dart:typed_data';

// defines how file should be which will be used for api prrocessing

class FileModel {
  final Uint8List bytes;
  final String name;

  FileModel({required this.bytes, required this.name});
}