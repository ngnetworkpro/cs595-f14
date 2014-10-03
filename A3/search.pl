#!/usr/bin/perl
# http://perl.about.com/od/filesystem/a/perl_parse_tabs.htm
use strict;
use warnings;

if (@ARGV) {
        my ($i,$input,$unique);
        $input = $ARGV[0];
        my @files = <files/*>;
        my $mapFile = "mapping.txt";
        foreach my $file (@files) {
                open (IN, "$file") or die  "couldn't open input file $file\n";
                $unique=0;
                while (my $line = <IN> ) {
                   chomp $line;
                   my @strings = $line =~ /$input/g;
                   foreach my $s (@strings) {
                        $unique++;
                   }
                }
                if($unique>0){
                        print $unique;
                        open (MAPFILE, "$mapFile") or die  "couldn't open input file $mapFile\n";
                        while(<MAPFILE>){
                          chomp;
                          my $f = substr($file, 6, 32); #http://perldoc.perl.org/functions/substr.html
                          (my $uri, my $name) = split("\t");
                          if($name =~ /$f/){
                              print "\t" . $uri . "\n";
                          }
                        }
                close(MAPFILE);
                }
        close(IN);
        }
}
exit;
