import com.aspose.words.Document;
import com.aspose.words.DocumentBuilder;
import com.aspose.words.JsonDataSource;
import com.aspose.words.ReportingEngine;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

// Helper for check_linq_runtime.py: builds templates, runs JSON reports, prints document text.
public class LinqHarness {
    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);
        switch (args[0]) {
            case "template": {
                List<String> lines = Files.readAllLines(Paths.get(args[2]), StandardCharsets.UTF_8);
                Document doc = new Document();
                DocumentBuilder builder = new DocumentBuilder(doc);
                for (int i = 0; i < lines.size(); i++) {
                    if (i < lines.size() - 1) {
                        builder.writeln(lines.get(i));
                    } else {
                        builder.write(lines.get(i));
                    }
                }
                doc.save(args[1]);
                break;
            }
            case "text": {
                out.print(new Document(args[1]).getText());
                break;
            }
            case "json": {
                Document doc = new Document(args[1]);
                JsonDataSource data = new JsonDataSource(args[2]);
                ReportingEngine engine = new ReportingEngine();
                if (args.length > 4) {
                    engine.buildReport(doc, data, args[4]);
                } else {
                    engine.buildReport(doc, data);
                }
                doc.save(args[3]);
                break;
            }
            default:
                throw new IllegalArgumentException("Unknown mode " + args[0]);
        }
    }
}
