{
  lib,
  # Builders
  buildPythonApplication,
  # Build system and dependencies
  hatchling,
  pygame,
}:

buildPythonApplication {
  pname = "skiing";
  version = "0.0.1";
  
  src = lib.fileset.toSource rec {
    root = ../../..;
    
    fileset = lib.fileset.unions (
      lib.map (lib.path.append root) [
        "./skiing"
        "./pyproject.toml"
        "./README.md"
        "./LICENSE"
      ]
    );
  };
  
  format = "pyproject";
  
  build-system = [
    hatchling
  ];
  
  dependencies = [
    pygame
  ];
}