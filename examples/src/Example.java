import com.aspose.words.Document;

// Compilation fixture. Build verification does not execute this program.
public class Example {
    public static void main(String[] args) throws Exception {
        Document document = new Document("input.docx");
        document.save("output.pdf");
    }
}
