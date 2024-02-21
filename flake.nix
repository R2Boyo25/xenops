{
  description = "A GUI editor with Nix integration";

  outputs = { self, nixpkgs, flake-utils }@inputs:
    let
      deps = pyPackages: with pyPackages; [
        pygame
      ];
      tools = pkgs: pyPackages: (with pyPackages; [
        pytest pytestCheckHook
        coverage pytest-cov
        mypy pytest-mypy
      ] ++ [pkgs.ruff]);

      xenops-package = {pkgs, python3Packages}:
        python3Packages.buildPythonPackage {
          pname = "xenops";
          version = "0.0.1";
          src = ./.;
          format = "pyproject";
          propagatedBuildInputs = deps python3Packages;
          nativeBuildInputs = [ python3Packages.setuptools ];
          checkInputs = tools pkgs python3Packages;
        };

      overlay = final: prev: {
        pythonPackagesExtensions =
          prev.pythonPackagesExtensions ++ [(pyFinal: pyPrev: {
            xenops = final.callPackage xenops-package {
              python3Packages = pyFinal;
            };
          })];
      };

      overlay-all = nixpkgs.lib.composeManyExtensions [
        overlay
      ];
    in
      flake-utils.lib.eachDefaultSystem (system:
        let
          pkgs = import nixpkgs { inherit system; overlays = [ overlay-all ]; };
          defaultPython3Packages = pkgs.python310Packages;  # force 3.10

          xenops = defaultPython3Packages.xenops;
          app = flake-utils.lib.mkApp { drv = xenops; };
        in
        {
          devShells.default = pkgs.mkShell {
            buildInputs = [(defaultPython3Packages.python.withPackages deps)];
            nativeBuildInputs = tools pkgs defaultPython3Packages;
            shellHook = ''
              export PYTHONASYNCIODEBUG=1
            '';
          };
          packages.xenops = xenops;
          packages.default = xenops;
          apps.xenops = app;
          apps.default = app;
        }
    ) // { overlays.default = overlay; };
}
