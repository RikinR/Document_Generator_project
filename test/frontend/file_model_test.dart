import 'dart:typed_data';
import 'package:document_generator/frontend/models/file_model.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('FileModel', () {
    test('constructor initializes properties correctly', () {
      final bytes = Uint8List.fromList([1, 2, 3]);
      const name = 'test_file.txt';

      final fileModel = FileModel(bytes: bytes, name: name);

      expect(fileModel.bytes, bytes);
      expect(fileModel.name, name);
    });
  });
}
