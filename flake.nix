{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = {nixpkgs, ...}: let
    supportedSystems = ["x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin"];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
  in {
    packages = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.python3Packages.buildPythonApplication {
        pname = "static-site-compiler";
        version = "0.1.0";

        src = ./.;

        pyproject = true;

        propagatedBuildInputs = with pkgs.python3Packages; [
          black
          jinja2
          markdown
          pygments
          python-frontmatter
          requests
          pytest
          expecttest
        ];

        build-system = with pkgs.python3Packages; [
          setuptools
        ];

        nativeCheckInputs = with pkgs.python3Packages; [
          pytestCheckHook
        ];

        meta.mainProgram = "ssc";
      };
    });

    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = with pkgs; [
          python3
          pyright
          python3Packages.black
          python3Packages.jinja2
          python3Packages.setuptools
          python3Packages.markdown
          python3Packages.pygments
          python3Packages.python-frontmatter
          python3Packages.requests
          python3Packages.pytest
          python3Packages.expecttest
        ];
      };
    });
  };
}
