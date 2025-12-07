{
  description = "A basic flake for Python development with Nix and NixOS";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    utils.url = "github:limwa/nix-flake-utils";

    # Needed for shell.nix
    flake-compat.url = "github:edolstra/flake-compat";
  };

  outputs = {
    self,
    nixpkgs,
    utils,
    ...
  }:
    utils.lib.mkFlakeWith {
      forEachSystem = system: {
        outputs = utils.lib.forSystem self system;

        pkgs = import nixpkgs {
          inherit system;
        };
      };
    } {
      formatter = {pkgs, ...}: pkgs.alejandra;
      
      packages = utils.lib.invokeAttrs {
        default = {outputs, ...}: outputs.packages.skiing;
        
        skiing = {pkgs, ...}: pkgs.python3.pkgs.callPackage ./nix/pkgs/skiing/package.nix {};
      };

      devShells = utils.lib.invokeAttrs {
        default = {outputs, ...}: outputs.devShells.python;

        # Python development shell
        python = {
          pkgs,
          ...
        }: let
          python = pkgs.python3.withPackages (ps: [
            ps.pygame
          ]);
        in
          pkgs.mkShell {
            meta.description = "A development shell with Python";

            packages = [
              python
            ];
          };
      };
    };
}
