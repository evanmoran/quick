#!/bin/sh
#
# curl github.com/evanmoran/quick/install.sh || sh
#
# Constants
# ------------------------------------------------------
INSTALL_DIR=${INSTALL_DIR:-"${HOME}/.quick"}
QUICK_URL="git://github.com/evanmoran/quick.git"
CACHE_URL="git://github.com/evanmoran/quick.wiki.git"
PREFIX=${PREFIX:-"/usr/local/bin"}

# Remove Previous Install
# ------------------------------------------------------

if [ -e "$INSTALL_DIR" ] || [ -e "$PREFIX/quick" ]; then
  echo "To continue, we must remove the following files:"
  [ -e "$INSTALL_DIR" ] && echo "  $INSTALL_DIR"
  [ -e "$PREFIX/quick" ] && echo "  $PREFIX/quick"
  printf "Remove these and continue? [Y/n] "
  read CHOICE

  # Default to 'y'
  CHOICE=${CHOICE:-y}

  if [ "$CHOICE" == "y" ] || [ "$CHOICE" == "Y" ]; then
    rm -rf "$INSTALL_DIR" "$PREFIX/quick"
  else
    echo "Stopping installation"
    exit
  fi

fi

# Install
# ------------------------------------------------------

echo "Installing to $INSTALL_DIR"

# Git clone source and cache
git clone -q "$QUICK_URL" "$INSTALL_DIR"
git clone -q "$CACHE_URL" "$INSTALL_DIR/cache"

echo "Linking to $PREFIX/quick"

# Create file executes python with cache directory (C_DIR)
cat > "$PREFIX/quick" <<EOF
#!/bin/sh

# Environment variable to QUICK_DIR
QUICK_DIR=\${QUICK_DIR:-"$INSTALL_DIR"}

# Execute quick
"\$QUICK_DIR/bin/quick"
EOF
chmod 755 "$PREFIX/quick"

# ln -s "$INSTALL_DIR/bin/quick" "$PREFIX/quick"

