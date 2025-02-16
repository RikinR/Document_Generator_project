// ignore_for_file: use_build_context_synchronously

import 'dart:typed_data';

import 'package:document_generator/frontend/viewmodels/file_viewmodel.dart';
import 'package:document_generator/frontend/views/pdf_preview_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// aka home screen this is what user sees first while landing .
// handles : file uploading , posting to api and pushing to processed pdf

class UploadFileScreen extends StatelessWidget {
  const UploadFileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text('Document Creator'),
        foregroundColor: Colors.white,
        centerTitle: true,
        backgroundColor: const Color.fromARGB(255, 59, 128, 219),
        elevation: 8,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(
            bottom: Radius.circular(12),
          ),
        ),
      ),
      body: ChangeNotifierProvider(
        create: (context) => FileViewModel(),
        child: Consumer<FileViewModel>(
          builder: (context, viewModel, child) {
            return Column(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: <Widget>[
                          Card(
                            elevation: 8,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Column(
                                children: [
                                  const Text(
                                    'Upload Files',
                                    style: TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 16),
                                  ElevatedButton.icon(
                                    onPressed: viewModel.pickFiles,
                                    icon: const Icon(Icons.upload_file),
                                    label: const Text('Select Files'),
                                    style: ElevatedButton.styleFrom(
                                      foregroundColor: Colors.white,
                                      backgroundColor: const Color.fromARGB(
                                          255, 59, 128, 219),
                                      padding: const EdgeInsets.symmetric(
                                          vertical: 16, horizontal: 24),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          if (viewModel.latexFiles.isNotEmpty ||
                              viewModel.pptFiles.isNotEmpty ||
                              viewModel.notebookFiles.isNotEmpty)
                            Card(
                              elevation: 8,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.all(16.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text(
                                      'Selected Files',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    const SizedBox(height: 8),
                                    if (viewModel.latexFiles.isNotEmpty)
                                      Column(
                                        children: viewModel.latexFiles
                                            .map((file) => ListTile(
                                                  leading: const Icon(
                                                      Icons.description),
                                                  title: Text(
                                                      'LaTeX File: ${file.name}'),
                                                ))
                                            .toList(),
                                      ),
                                    if (viewModel.pptFiles.isNotEmpty)
                                      Column(
                                        children: viewModel.pptFiles
                                            .map((file) => ListTile(
                                                  leading: const Icon(
                                                      Icons.slideshow),
                                                  title: Text(
                                                      'PPT File: ${file.name}'),
                                                ))
                                            .toList(),
                                      ),
                                    if (viewModel.notebookFiles.isNotEmpty)
                                      Column(
                                        children: viewModel.notebookFiles
                                            .map((file) => ListTile(
                                                  leading:
                                                      const Icon(Icons.code),
                                                  title: Text(
                                                      'Notebook File: ${file.name}'),
                                                ))
                                            .toList(),
                                      ),
                                    const SizedBox(height: 16),
                                    ElevatedButton.icon(
                                      onPressed: viewModel.clearFiles,
                                      icon: const Icon(Icons.clear),
                                      label: const Text('Clear Files'),
                                      style: ElevatedButton.styleFrom(
                                        foregroundColor: Colors.white,
                                        backgroundColor: Colors.red,
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 16, horizontal: 24),
                                        shape: RoundedRectangleBorder(
                                          borderRadius:
                                              BorderRadius.circular(8),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
                  ),
                ),
                if (viewModel.isProcessing)
                  const Center(
                    child: CircularProgressIndicator(),
                  )
                else if (viewModel.latexFiles.isEmpty &&
                    viewModel.pptFiles.isEmpty &&
                    viewModel.notebookFiles.isEmpty)
                  const Center(
                    child: Text('No files selected.'),
                  )
                else
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: ElevatedButton.icon(
                      onPressed: () async {
                        try {
                          Uint8List pdfBytes = await viewModel.uploadFiles();
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => PdfPreviewScreen(
                                pdfBytes: pdfBytes,
                                fileName: 'CompiledFile',
                              ),
                            ),
                          );
                        } catch (e) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Error: $e')),
                          );
                        }
                      },
                      icon: const Icon(Icons.cloud_upload),
                      label: const Text('Process Files'),
                      style: ElevatedButton.styleFrom(
                        foregroundColor: Colors.white,
                        backgroundColor:
                            const Color.fromARGB(255, 59, 128, 219),
                        padding: const EdgeInsets.symmetric(
                            vertical: 16, horizontal: 24),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
