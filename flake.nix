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

        propagatedBuildInputs = with pkgs.python3Packages; [
          black
          certifi
          charset-normalizer
          click
          idna
          importlib-metadata
          jinja2
          markdown
          markupsafe
          mypy-extensions
          pathspec
          platformdirs
          pygments
          python-frontmatter
          pyyaml
          requests
          tomli
          typed-ast
          typing-extensions
          urllib3
          zipp
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
          python3Packages.black
          python3Packages.jinja2
          python3Packages.markdown
          python3Packages.requests
          python3Packages.pyyaml
        ];
      };
    });
  };
}
