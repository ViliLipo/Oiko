# Oiko Finnish Spellchecker for Neovim

## Toiminta

Oiko sovittaa Voikko-kielioppikirjaston Python-version NeoVim-pluginiksi.
Toiminnallisuuksiltaan plugin vastaa Vimchantia.
Huomattavin ero VimChantiin on, että Oiko ei vaadi enchant ohjelmistoa,
mutta Oiko tukee vain suomenkieltä. Oiko ei myöskään tue tavallista
Vimiä, koska se on rakennettu NeoVimin remote-plugin rajapintaa hyödyntäen.

## Commands

- OikoOn
  - Oikoluku menee päälle. Tarkistus ajetaan, kun normaalitilasta poistutaan.
    Oiko tunnistaa vain yksittäisten sanojen kirjoitusvirheet, ei muita
    rakenteellisia kielioppivirheitä, tai yhdyssanavirheitä.
- OikoOff
  - Oikoluku sammutetaan
- OikoClear
  - Poistaa highlight merkinnät.
- OikoSpell
  - Ajaa oikoluvun kerran.

