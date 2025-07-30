.DELETE_ON_ERROR:


all:  ../data/test.ttl 

%.ttl: cityrdf_typedGenAttrs-withIDs-citygml3.xsparql %.gml
	xsparql cityrdf_typedGenAttrs-withIDs-citygml3.xsparql input=$*.gml -f TEMP.ttl > /dev/null
	 riot --syntax ttl --formatted ttl --base "https://example.com/resource/case1/ifc/" TEMP.ttl |\
	 perl -00e '@a=<>; print shift @a; print sort @a' > $*.ttl
	rm TEMP.ttl
	python CleanAndLowercasePrefixes.py $(abspath $*.ttl) $(abspath $*.ttl) 
