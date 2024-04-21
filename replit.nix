{ pkgs }: {
  deps = [
    pkgs.python311Packages.jupyter_core
    pkgs.zulu8
    pkgs.bash
  ];
}