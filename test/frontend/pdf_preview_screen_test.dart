import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:document_generator/frontend/views/pdf_preview_screen.dart';
import 'package:document_generator/frontend/views/upload_file_screen.dart';

void main() {
  late Uint8List dummyPdfBytes;

  setUp(() {
    dummyPdfBytes = Uint8List.fromList([0, 1, 2, 3]);
  });

  group('PdfPreviewScreen Widget Tests', () {
    testWidgets('Displays buttons and text', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: Text('Skipped due to non-web environment'),
          ),
        ),
      );


      if (!isWeb) {
        return;
      }

      await tester.pumpWidget(
        MaterialApp(
          home: PdfPreviewScreen(pdfBytes: dummyPdfBytes),
        ),
      );

      expect(find.text('Download PDF or Click to Preview'), findsOneWidget);
      expect(find.text('Download PDF'), findsOneWidget);
      expect(find.text('Preview the file!'), findsOneWidget);
      expect(find.text('Create New Document'), findsOneWidget);
    });

    testWidgets(
        'Navigates to UploadFileScreen when "Create New Document" is pressed',
        (WidgetTester tester) async {
      if (!isWeb) {
        return;
      }

      await tester.pumpWidget(
        MaterialApp(
          home: PdfPreviewScreen(pdfBytes: dummyPdfBytes),
        ),
      );

      await tester.tap(find.text('Create New Document'));
      await tester.pumpAndSettle();

      expect(find.byType(UploadFileScreen), findsOneWidget);
    });
  });
}

bool get isWeb => identical(0, 0.0);
