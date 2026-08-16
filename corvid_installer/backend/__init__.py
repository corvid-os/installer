"""Real install logic, no GUI in here -- everything is a plain function
that shells out to standard Arch install tools. Every function takes a
`dry_run` flag and a `log` callback (message -> None); when dry_run is
True, commands are logged but never executed. Nothing in this package
runs unless the installer's Progress step calls it, and that only
happens when you click through the full wizard against a real disk."""
