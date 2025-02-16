import 'dart:typed_data';
import 'package:document_generator/frontend/models/file_model.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

// this service file connects to our api endpoint and uses http to send rest api requests .

class ApiService {
  final String _apiUrl = dotenv.env['API_URL'] ?? '';

  Future<Uint8List> uploadFiles(List<FileModel> latexFiles, List<FileModel> pptFiles, List<FileModel> notebookFiles) async {
    var request = http.MultipartRequest('POST', Uri.parse('$_apiUrl/process/'));

    for (var file in latexFiles) {
      request.files.add(http.MultipartFile.fromBytes('latex', file.bytes, filename: file.name));
    }

    for (var file in pptFiles) {
      request.files.add(http.MultipartFile.fromBytes('ppt', file.bytes, filename: file.name));
    }

    for (var file in notebookFiles) {
      request.files.add(http.MultipartFile.fromBytes('notebook', file.bytes, filename: file.name));
    }

    var response = await request.send();

    if (response.statusCode == 200) {
      return await response.stream.toBytes();
    } else {
      throw Exception('Failed to upload files');
    }
  }
}