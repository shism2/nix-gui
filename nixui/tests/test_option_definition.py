from nixui.options.option_definition import OptionDefinition, Undefined
from nixui.options import nix_eval


def test_expr_string_from_obj():
    d = OptionDefinition.from_object(True)
    assert d.expression_string.strip() == "true"


def test_obj_from_expr_string():
    d = OptionDefinition.from_expression_string('if true then "bla" else "foo"')
    assert d.obj == "bla"


def test_equality_undefined():
    assert OptionDefinition.from_object(Undefined) == OptionDefinition.from_object(Undefined)


def test_import_path():
    d = OptionDefinition.from_expression_string(
        """[
        ./hardware-configuration.nix
        ]""",
        context={'module_dir': '/foo'},
    )
    assert len(d.obj) == 1
    assert d.obj[0].eval_full_path() == '/foo/hardware-configuration.nix'


def test_import_path_nixpkgs():
    nixpkgs_path = nix_eval.resolve_nix_search_path('<nixpkgs>')
    d = OptionDefinition.from_expression_string(
        """[
        <nixpkgs/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix>
        ]""",
        context={'module_dir': '/foo'},  # unused, but required arg
    )
    assert len(d.obj) == 1
    assert d.obj[0].eval_full_path() == f'{nixpkgs_path}/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix'
