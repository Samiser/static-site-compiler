{
  description = "A Docker image for a static site with a Python generator";

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

        staticSite = pkgs.stdenv.mkDerivation {
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

        staticAssets = pkgs.stdenv.mkDerivation {
          name = "static-assets";
          src = ./static;

          installPhase = ''
            runHook preInstall
            mkdir -p $out
            cp -r ./* $out
            runHook postInstall
          '';
        };

        nginxWebRoot = pkgs.stdenv.mkDerivation {
          name = "web-root";
          src = ./.;

          buildPhase = ''
            mkdir -p $out
            cp -r ${staticSite}/* $out
            cp -r ${staticAssets}/* $out
          '';
        };

        # nginxWebRoot = pkgs.writeTextDir "index.html" (builtins.readFile "${staticSite}/index.html");

        nginxConf = pkgs.writeText "nginx.conf" ''
          user nobody nobody;
          daemon off;
          error_log /dev/stdout info;
          pid /dev/null;
          events {}
          http {
            include ${pkgs.nginx}/conf/mime.types;
            access_log /dev/stdout;
            server {
              listen 80;
              index index.html;
              location / {
                root ${nginxWebRoot};
              }
            }
          }
        '';

        staticSiteImage = pkgs.dockerTools.buildLayeredImage {
          name = "static-site";
          tag = "latest";
          contents = [ pkgs.fakeNss pkgs.nginx pkgs.busybox ];
          extraCommands = ''
            mkdir -p tmp/nginx_client_body
            mkdir -p var/log/nginx
            mkdir -p var/cache/nginx
          '';
          config = {
            Cmd = [ "nginx" "-c" "${nginxConf}" ];
            ExposedPorts = {
              "80/tcp" = {};
            };
          };
        };
      in
      {
        packages.default = staticSite;
        packages.dockerImage = staticSiteImage;
      }
    );
}

