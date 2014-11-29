# Fool
[![Build Status](https://travis-ci.org/nathantypanski/fool.svg)](https://travis-ci.org/nathantypanski/fool)
[![Documentation Status](https://readthedocs.org/projects/fool/badge/?version=latest)](https://readthedocs.org/projects/fool/?badge=latest)

bootstrap your dotfiles like a fool

- [api docs](http://fool.readthedocs.org/en/latest/)

![the fool tarot card](doc/source/_static/fool.jpg)


## Use case

Just like everybody else, you decide to keep your dotfiles somewhere reproducible, perhaps in a VCS like [Git](http://git-scm.com/).

Just like everybody else, I wrote my own dotfile manager script bundle. It's called Fool.
You're reading about it.

## Ok, really, what's the use case?

Say you work on 5 different computers. You put all your dotfiles in one repo, so hopefully you can clone them around nicely.

But wait. You can't do that because half of them don't apply to the server you're working on. You just need your `.vimrc` and you're golden.

Bam! Enter Fool.

## Features

- [x] [XDG Base Directory](http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html) conformance - manage your Fool configs with Fool
- [x] Python 2.7 and Python 3.3 compatibility
- [ ] Automatically symlink your dotfiles
- [ ] Manage multiple overlapping sections of dotfiles

## FAQ

### Hey! This doesn't do anything!?

I'm still writing it. Be patient.

### How is this better than handrolling bash scripts?

It's not. It's probably worse. Fool is written in Python, and it doesn't do
anything yet. See my above answer.

## Design

> **Warning**: This is incomplete and subject to change. It might describe things that have not been implemented yet. Proceed with a bucket of salt.

### Sections

A Fool **Section** is a collection of files that all get symlinked to one place.

For example, say you have your Vim configs in a folder.

```
./vim/.vimrc
      .vim/
```

That's a great start for a Fool Section called `vim`.

```
$ cd ~/dotfiles/vim
~/dotfiles/vim $ fool section init vim --source="./vim" --target="~/"
```

That creates a section called `vim`, located at `./vim`, with a target of `~/`.

Now you have the following in your fool config:

```
./fool/sections/vim/source -> ../../../vim
                    target -> ~/
```

You've probably noticed something by now. Fool uses the POSIX filesystem as a database. Symlinks are how it finds its way around the world.

### Chapters

Chapters are collections of Sections. That probably doesn't surprise you, because books have chapters also and these chapters contain sections.
