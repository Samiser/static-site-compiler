{
  description = "A static site generator in Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          markdown
          jinja2
          pyyaml
          python-frontmatter
          requests
        ]);
      in {
        packages.default = pkgs.stdenv.mkDerivation {
          name = "static-site-generator";
          src = ./.;
          buildInputs = [ pythonEnv ];

          buildPhase = ''
            runHook preBuild
            python build.py
            runHook postBuild
          '';

          installPhase = ''
            runHook preInstall
            mkdir -p $out
            cp index.html $out/
            runHook postInstall
          '';
        };
      }
    );
}

