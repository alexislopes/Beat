import java.util.ArrayList;

public class Python {
    private ArrayList<String> links;

    public Python() {
        links = new ArrayList<>();
        addLinks();
    }

    String livros = "\t   Livros:\nhttps://goo.gl/S2Nt5a\n\n";
    String videos = "\t   Videos:\nhttps://goo.gl/wR6jGm\nhttps://goo.gl/2sQMnn\n\n";



    public void addLinks(){
        links.add(livros);
        links.add(videos);
    }

    public void imprimir(){
        for (String link: links) {
            System.out.println(link);
        }
    }



    public ArrayList<String> getLinks() {
        return links;
    }

    public void setLinks(ArrayList<String> links) {
        this.links = links;
    }







}
