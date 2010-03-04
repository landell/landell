AC_PREREQ([2.65])

AC_INIT([sltv], [0.5], [sltv-dev@listas.softwarelivre.org])

AC_CONFIG_MACRO_DIR([m4])

AC_CONFIG_SRCDIR([configure.ac])

AC_PROG_INSTALL

AM_INIT_AUTOMAKE([-Wall -Werror])

AM_PATH_PYTHON(2.4.0)

dnl expanding useful variables
AS_AC_EXPAND(LIBDIR, $libdir)
AS_AC_EXPAND(BINDIR, $bindir)
AS_AC_EXPAND(DATADIR, $datarootdir)

AC_CONFIG_FILES([
        Makefile
        ui/Makefile
	ui/input/Makefile
	ui/output/Makefile
	sltv/input/Makefile
	sltv/output/Makefile
	sltv/encoding/Makefile
	sltv/ui/Makefile
	sltv/ui/input/Makefile
        sltv/Makefile
        sltv/settings.py
	src/Makefile
        src/sltv
	man/Makefile
])

AC_OUTPUT
