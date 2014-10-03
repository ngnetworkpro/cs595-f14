private static String getHash(String uri, PrintWriter map) throws IOException{
        //http://www.mkyong.com/java/java-sha-hashing-example/
        StringBuilder sb = new StringBuilder();
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(uri.getBytes());
            byte byteData[] = md.digest();
            for (int i = 0; i < byteData.length; i++) {
                sb.append(Integer.toString((byteData[i] & 0xff) + 0x100, 16).substring(1));
            }
        } catch (NoSuchAlgorithmException ex) {
            Logger.getLogger(getDownload.class.getName()).log(Level.SEVERE, null, ex);
        }
        map.println(uri + "\t" + sb.toString());
        return sb.toString();
    }