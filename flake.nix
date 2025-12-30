{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = {
    nixpkgs,
    self,
    ...
  }: let
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

        dependencies = with pkgs.python3Packages; [
          jinja2
          markdown
          pygments
          python-frontmatter
          requests
        ];

        build-system = with pkgs.python3Packages; [
          setuptools
        ];

        nativeCheckInputs = with pkgs.python3Packages; [
          pytestCheckHook
          expecttest
        ];

        meta.mainProgram = "ssc";
      };
    });

    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      pkg = self.packages.${system}.default;
    in {
      default = pkgs.mkShell {
        inputsFrom = [pkg];
        packages = with pkgs; [
          pyright
          python3Packages.black
          python3Packages.pytest
          python3Packages.expecttest
        ];
      };
    });
  };
}
