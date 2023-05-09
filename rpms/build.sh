SRC_DIR=$HOME/rpmbuild/SOURCES/vlmcsd-svn1113.tar.gz
wget -O $SRC_DIR https://github.com/simaek/vlmcsd/archive/refs/tags/svn1113.tar.gz
rpmbuild -bb --nodebuginfo vlmcsd.spec
