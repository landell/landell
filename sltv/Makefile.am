SUBDIRS = input ui

sltvdir = $(bindir)
bin_SCRIPTS = sltv

sltvlibdir = $(libdir)/sltv
sltvlib_DATA = about.py effects.py output.py	\
	settings.py sltv_ui.py swap.py		\
	audio.py edit_source.py encoding.py preview.py		\
	sltv.py sources.py videomixer.py		\
	registry.py factory.py

EXTRA_DIST = $(bin_SCRIPTS) $(sltvlib_DATA)

DISTCLEANFILES = settings.py
