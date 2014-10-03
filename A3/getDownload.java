/*
 * Uses boilerplate to download URL and remove the HTML markup.
 * https://code.google.com/p/boilerpipe/
 * Documentation at 
 * http://boilerpipe.googlecode.com/svn/trunk/boilerpipe-core/javadoc/1.0/index.html
 */
/**
 *
 * @author sybil melton
 */
import org.xml.sax.InputSource;

import de.l3s.boilerpipe.document.TextDocument;
import de.l3s.boilerpipe.extractors.ArticleExtractor;
import de.l3s.boilerpipe.sax.BoilerpipeSAXInput;

import java.io.InputStream;
import java.net.URL;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class getDownload {
    public static void main(final String[] args) throws Exception {

        String inFile = args[0];
        String u = "";
        out = null;
        map = new PrintWriter(new BufferedWriter
                        (new FileWriter("mapping.txt")));
        String outFile = "";
        BufferedReader file = new BufferedReader(new FileReader(inFile));
            String text = "";
            while (file.ready()) {
                text = file.readLine();
                u = "http://" + text;
                //Hash the URI to get the filename it will be output to
                outFile = "./files/"+getHash(text, map);
                System.out.println(text);
                //set URL for boilerplate to fetch
                URL url;
                url = new URL(u);
                
                final TextDocument doc;
              try{  
                InputStream urlStream = url.openStream();
                final InputSource is = new InputSource(urlStream);
                final BoilerpipeSAXInput in = new BoilerpipeSAXInput(is);
                doc = in.getTextDocument();

                //http://www.cs.carleton.edu/faculty/dmusican/cs117s03/iocheat.html
                    try{
                        out = new PrintWriter(new BufferedWriter
                                (new FileWriter(outFile)));
                        out.println(ArticleExtractor.INSTANCE.getText(doc));
                    }catch(FileNotFoundException e){
                        System.out.println(e);
                    }catch(SecurityException e) {
                        System.out.println(e);
                        System.out.println("ERROR: couldn't open URL " + url);
                    }finally {
                        if(out != null){
                            out.close();
                        }
                    }
              }catch(IOException e) {
                   System.out.println("ERROR: couldn't open URL " + url);
                }
        }
        map.close();
    }
    private static PrintWriter out;   
    private static PrintWriter map;
}
