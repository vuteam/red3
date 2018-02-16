installdir = $(pkglibdir)/python/Plugins/Extensions

SUBDIRS = TuxboxPlugins CutListEditor PicturePlayer MediaScanner MediaPlayer GraphMultiEPG SocketMMI DVDBurn \
	BhEpgBackup BhFullBackup BhFastEpg DLNABrowser DLNAServer \
        BhPersonalBackup BhWeather SatipClient StreamTV

if HAVE_LIBDDVD
SUBDIRS += DVDPlayer
endif

install_PYTHON =	\
	__init__.py
