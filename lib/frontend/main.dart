import 'package:document_generator/frontend/viewmodels/file_viewmodel.dart';
import 'package:document_generator/frontend/views/upload_file_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';


// main file or entrance point to our flutter frontend
void main() async {
  await dotenv.load(fileName: ".env");
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChangeNotifierProvider(
        create: (context) => FileViewModel(),
        child: const UploadFileScreen(),
      ),
    );
  }
}
