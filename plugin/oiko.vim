
if (exists('g:loaded_oiko') && g:loaded_oiko) || &cp
  finish
endif

hi def OikoError gui=undercurl cterm=undercurl guifg=red ctermfg=red

let g:loaded_oiko = 1
