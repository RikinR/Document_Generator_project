// ignore_for_file: prefer_final_fields, use_rethrow_when_possible

import 'dart:typed_data';
import 'package:document_generator/frontend/models/file_model.dart';
import 'package:document_generator/frontend/services/api_service.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

// this is like the functional file . it manages state throughout the webapp
// utilizes provider for state management.
// conatins key functions

class FileViewModel with ChangeNotifier {
  final ApiService apiService;

  FileViewModel() : apiService = ApiService();

  set apiService(ApiService apiService) {
    apiService = apiService;
  }

  List<FileModel> _latexFiles = [];
  List<FileModel> _pptFiles = [];
  List<FileModel> _notebookFiles = [];
  bool _isProcessing = false;

  List<FileModel> get latexFiles => _latexFiles;
  List<FileModel> get pptFiles => _pptFiles;
  List<FileModel> get notebookFiles => _notebookFiles;
  bool get isProcessing => _isProcessing;

  Future<void> pickFiles() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['tex', 'pptx'], // currently 'ipynb' is removed
      allowMultiple: true,
      withData: true,
    );

    if (result != null) {
      for (var file in result.files) {
        if (file.bytes != null) {
          FileModel fileModel = FileModel(bytes: file.bytes!, name: file.name);
          if (file.extension == 'tex') {
            _latexFiles.add(fileModel);
          } else if (file.extension == 'pptx') {
            _pptFiles.add(fileModel);
          } else if (file.extension == 'ipynb') {
            _notebookFiles.add(fileModel);
          }
        }
      }
      notifyListeners();
    }
  }

  Future<Uint8List> uploadFiles() async {
    _isProcessing = true;
    notifyListeners();

    try {
      Uint8List pdfBytes =
          await apiService.uploadFiles(_latexFiles, _pptFiles, _notebookFiles);
      _isProcessing = false;
      notifyListeners();
      return pdfBytes;
    } catch (e) {
      _isProcessing = false;
      notifyListeners();
      throw e;
    }
  }

  void clearFiles() {
    _latexFiles.clear();
    _pptFiles.clear();
    _notebookFiles.clear();
    notifyListeners();
  }
}
