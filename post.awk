{
    if($2 == "[]") {
        print "{ \"word\":\"" $1 "\", \"dict\":[] }"
    } else {
        a=$1;
        $1 = "";
        print "{ \"word\": \"" a "\", \"dict\":" $0 " }"
    }
}
