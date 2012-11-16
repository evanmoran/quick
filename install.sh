#!/bin/sh
#
# Install quick with curl
# curl
#
#
#
# Constants
# ------------------------------------------------------
INSTALL_DIR=${INSTALL_DIR:-"${HOME}/.quick"}
QUICK_URL="git://github.com/evanmoran/quick.git"
CACHE_URL="git://github.com/evanmoran/quick.wiki.git"

#
# Setup
# ------------------------------------------------------

if [ -d "$INSTALL_DIR" ]; then
  echo "Previous install already found at $INSTALL_DIR"
  printf "Remove this install and continue? [Y/n] "
  read CHOICE

  # Default to 'y'
  CHOICE=${CHOICE:-y}

  if [ "$CHOICE" == "y" ] || [ "$CHOICE" == "Y" ]; then
    rm -rf "$INSTALL_DIR"
  else
    echo "Stopping installation"
    exit
  fi

fi

echo "Installing in $INSTALL_DIR"

git clone "$QUICK_URL" "$INSTALL_DIR"
git clone "$CACHE_URL" "$INSTALL_DIR/cache"
