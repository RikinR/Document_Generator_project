import 'dart:typed_data';
import 'package:document_generator/frontend/models/file_model.dart';
import 'package:document_generator/frontend/viewmodels/file_viewmodel.dart';
import 'package:document_generator/frontend/views/upload_file_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';
import 'upload_file_screen.mocks.dart';

@GenerateMocks([FileViewModel])
void main() {
  late MockFileViewModel mockViewModel;

  setUp(() {
    mockViewModel = MockFileViewModel();
  });

  Widget createTestWidget() {
    return MaterialApp(
      home: ChangeNotifierProvider<FileViewModel>.value(
        value: mockViewModel,
        child: const UploadFileScreen(),
      ),
    );
  }

  group('UploadFileScreen UI Tests', () {
    testWidgets('Displays title and buttons correctly',
        (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());

      expect(find.text('Document Creator'), findsOneWidget);

      expect(find.text('Select Files'), findsOneWidget);

      expect(find.text('Process Files'), findsNothing);
    });

    testWidgets('Displays selected files list when files are added',
        (WidgetTester tester) async {
      when(mockViewModel.latexFiles).thenReturn([
        FileModel(bytes: Uint8List(0), name: 'file1.tex'),
      ]);
      when(mockViewModel.pptFiles).thenReturn([]);
      when(mockViewModel.notebookFiles).thenReturn([]);

      await tester.pumpWidget(createTestWidget());
      await tester.pump();

      expect(find.text('LaTeX File: file1.tex'), findsOneWidget);
    });

    testWidgets('Tapping "Select Files" triggers pickFiles()',
        (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());

      await tester.tap(find.text('Select Files'));
      await tester.pump();

      verify(mockViewModel.pickFiles()).called(1);
    });

    testWidgets('Process Files button calls uploadFiles and navigates',
        (WidgetTester tester) async {
      when(mockViewModel.latexFiles).thenReturn([
        FileModel(bytes: Uint8List(0), name: 'file1.tex'),
      ]);
      when(mockViewModel.pptFiles).thenReturn([]);
      when(mockViewModel.notebookFiles).thenReturn([]);
      when(mockViewModel.uploadFiles()).thenAnswer((_) async => Uint8List(10));

      await tester.pumpWidget(createTestWidget());
      await tester.pump();

      await tester.tap(find.text('Process Files'));
      await tester.pump();

      verify(mockViewModel.uploadFiles()).called(1);
    });

    testWidgets('Shows CircularProgressIndicator while processing',
        (WidgetTester tester) async {
      when(mockViewModel.isProcessing).thenReturn(true);

      await tester.pumpWidget(createTestWidget());
      await tester.pump();

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('Shows error Snackbar if upload fails',
        (WidgetTester tester) async {
      when(mockViewModel.uploadFiles()).thenThrow(Exception('Upload failed'));
      when(mockViewModel.latexFiles).thenReturn([
        FileModel(bytes: Uint8List(0), name: 'file1.tex'),
      ]);

      await tester.pumpWidget(createTestWidget());
      await tester.pump();

      await tester.tap(find.text('Process Files'));
      await tester.pumpAndSettle();

      expect(find.textContaining('Error:'), findsOneWidget);
    });
  });
}
