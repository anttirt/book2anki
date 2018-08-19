package net.anttirt;

import java.util.Scanner;
import java.io.IOException;
import java.util.List;
import java.util.Arrays;
import java.util.stream.Collectors;

import com.atilika.kuromoji.TokenBase;
import com.atilika.kuromoji.TokenizerBase;


public class WordExtract {
    public static void main(String[] args) throws IOException {
        var sc = new Scanner(System.in);
        var sb = new StringBuilder();

        String dict = "ipadic";
        boolean showAllFeatures = false;
        List<Integer> selectedFeatures = null;

        {
            boolean nextIsFeaturesArray = false;
            for(String arg : args) {
                if(nextIsFeaturesArray) {
                    nextIsFeaturesArray = false;
                    selectedFeatures = Arrays.asList(arg.split(",")).stream()
                        .map(s -> Integer.parseInt(s))
                        .collect(Collectors.toList());
                }
                else if(arg.equals("--all"))
                    showAllFeatures = true;
                else if(arg.equals("--features"))
                    nextIsFeaturesArray = true;
                else
                    dict = arg;
            }
        }

        TokenizerBase tokenizer;

        switch(dict)
        {
            case "ipadic":            tokenizer = new com.atilika.kuromoji.ipadic.Tokenizer(); break;
            // case "ipadic-neologd":    tokenizer = new com.atilika.kuromoji.ipadic.neologd.Tokenizer(); break;
            case "jumandic":          tokenizer = new com.atilika.kuromoji.jumandic.Tokenizer(); break;
            case "naist-jdic":        tokenizer = new com.atilika.kuromoji.naist.jdic.Tokenizer(); break;
            case "unidic":            tokenizer = new com.atilika.kuromoji.unidic.Tokenizer(); break;
            case "unidic-kanaaccent": tokenizer = new com.atilika.kuromoji.unidic.kanaaccent.Tokenizer(); break;
            // case "unidic-neologd":    tokenizer = new com.atilika.kuromoji.unidic.neologd.Tokenizer(); break;
            default:
                System.err.println("Unrecognized dictionary " + dict);
                System.err.println("Known dictionaries:");
                System.err.println("\tipadic");
                // System.err.println("\tipadic-neologd");
                System.err.println("\tjumandic");
                System.err.println("\tnaist-jdic");
                System.err.println("\tunidic");
                System.err.println("\tunidic-kanaaccent");
                // System.err.println("\tunidic-neologd");
                tokenizer = null;
                System.exit(1);
                break;
        }

        var done = false;

        while(!done) {
            String text = null;
            try {
                String line = sc.nextLine();
                int ix = line.indexOf('。');
                int sblen = sb.length();
                sb.append(line);
                if(ix != -1) {
                    text = sb.substring(0, sblen + ix + 1);
                    sb.delete(0, sblen + ix + 1);
                }
            }
            catch(java.util.NoSuchElementException e) {
                text = sb.toString();
                done = true;
            }

            if(text != null) {
                for (TokenBase token : tokenizer.tokenize(text)) {
                    if(showAllFeatures) {
                        System.out.println(token.getSurface() + "\t" + token.getAllFeatures());
                    }
                    else if (selectedFeatures != null) {
                        var features = token.getAllFeaturesArray();
                        sb.setLength(0);
                        sb.append(token.getSurface());
                        sb.append("\t");
                        String intr = "";
                        for(Integer feature : selectedFeatures) {
                            sb.append(intr);
                            sb.append(features[feature]);
                            intr = ",";
                        }
                        System.out.println(sb.toString());
                    }
                    else {
                        var features = token.getAllFeaturesArray();
                        String partOfSpeech = features[0];
                        switch(partOfSpeech) {
                            case "動詞":
                            case "形容詞": {
                                // for verbs and adjectives print the base form
                                int dashIndex = features[7].indexOf('-');
                                if(dashIndex != -1)
                                    System.out.println(features[7].substring(0, dashIndex));
                                else
                                    System.out.println(features[7]);
                            } break;

                            case "名詞":
                                if(features[1].equals("固有名詞")) {
                                    // names are printed as-is
                                    System.out.println(token.getSurface());
                                }
                                else {
                                    // wasei-eigo have the english word in field 7,
                                    // so we use field 8 for those instead
                                    boolean foundAscii = false;
                                    int dashIndex = -1;
                                    var baseForm = features[7];
                                    for(int i = 0; i < baseForm.length(); ++i) {
                                        char c = baseForm.charAt(i);
                                        if(c == '-')
                                            dashIndex = i;

                                        if(c >= 'a' && c <= 'z') {
                                            foundAscii = true;
                                            break;
                                        }
                                    }
                                    if(foundAscii)
                                        System.out.println(features[8]);
                                    else if(dashIndex != -1)
                                        System.out.println(features[7].substring(0, dashIndex));
                                    else
                                        System.out.println(token.getSurface());
                                }
                                break;

                            default:
                                break;

                        }
                    }
                }
            }
        }
    }
}
