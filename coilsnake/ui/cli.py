#! /usr/bin/env python
import argparse
import logging

from coilsnake.ui.common import compile_project, decompile_rom, upgrade_project, decompile_script, patch_rom, setup_logging
from coilsnake.ui.information import coilsnake_about


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--quiet", help="silence all output", action="store_true")
    subparsers = parser.add_subparsers()
    subparsers.required = True

    compile_parser = subparsers.add_parser("compile", help="compile from project to rom")
    compile_parser.add_argument("project_directory")
    compile_parser.add_argument("base_rom")
    compile_parser.add_argument("output_rom")
    compile_parser.set_defaults(func=_compile)

    decompile_parser = subparsers.add_parser("decompile", help="decompile from rom to project")
    decompile_parser.add_argument("rom")
    decompile_parser.add_argument("project_directory")
    decompile_parser.set_defaults(func=_decompile)

    upgrade_parser = subparsers.add_parser("upgrade",
                                           help="upgrade a project which was created by an older version of CoilSnake")
    upgrade_parser.add_argument("base_rom")
    upgrade_parser.add_argument("project_directory")
    upgrade_parser.set_defaults(func=_upgrade)
    
    decomp_script_parser = subparsers.add_parser("scriptdump", help="Decompile a ROM's script to an already existing project.")
    
    decomp_script_parser.add_argument("rom_filename")
    decomp_script_parser.add_argument("project_directory")
    decomp_script_parser.set_defaults(func=_scriptdump)
    
    patch_rom_parser = subparsers.add_parser("patchrom", help="Apply an EBP or IPS patch to a ROM (for headered give true or false)")
    
    patch_rom_parser.add_argument("clean_rom")
    patch_rom_parser.add_argument("output_rom")
    patch_rom_parser.add_argument("patch")
    patch_rom_parser.add_argument("headered")
    patch_rom_parser.set_defaults(func=_patchrom)

    version_parser = subparsers.add_parser("version", help="display version information")
    version_parser.set_defaults(func=_version)

    args = parser.parse_args()

    setup_logging(quiet=args.quiet, verbose=args.verbose)

    args.func(args)


def _compile(args):
    compile_project(project_path=args.project_directory,
                    base_rom_filename=args.base_rom,
                    output_rom_filename=args.output_rom)


def _decompile(args):
    decompile_rom(rom_filename=args.rom,
                  project_path=args.project_directory)


def _upgrade(args):
    upgrade_project(base_rom_filename=args.base_rom,
                    project_path=args.project_directory)

def _scriptdump(args):
	decompile_script(rom_filename=args.rom_filename, 
					 project_path=args.project_directory)

def _patchrom(args):
	patch_rom(clean_rom_filename=args.clean_rom,
			  patched_rom_filename=args.output_rom,
			  patch_filename=args.patch,
			  headered=args.headered)


def _version(args):
    print(coilsnake_about())


