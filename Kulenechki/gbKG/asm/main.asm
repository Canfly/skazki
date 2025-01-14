SECTION "Header", ROM0[$0100]
    nop
    jp Start
    db "Game Title   ",0,0,0
    dw $FFFF, $FFFF

SECTION "Tile Data", ROM0[$8000] ; Помещаем данные символов для "CANFLY" сюда

CANFLY_TILES:
; 'C'
    db %00111100
    db %01100010
    db %01000000
    db %01000000
    db %01000000
    db %01100010
    db %00111100
    db %00000000
; 'A'
    db %00111100
    db %01000010
    db %01000010
    db %01111110
    db %01000010
    db %01000010
    db %01000010
    db %00000000
; 'N'
    db %01000010
    db %01100010
    db %01010010
    db %01001010
    db %01000110
    db %01000010
    db %01000010
    db %00000000
; 'F'
    db %01111110
    db %01000000
    db %01000000
    db %01111100
    db %01000000
    db %01000000
    db %01000000
    db %00000000
; 'L'
    db %01000000
    db %01000000
    db %01000000
    db %01000000
    db %01000000
    db %01000000
    db %01111110
    db %00000000
; 'Y'
    db %01000010
    db %01000010
    db %01000010
    db %00111100
    db %00001000
    db %00001000
    db %00111100
    db %00000000

SECTION "Main", ROM0[$0150]
Start:
    ; Включаем LCD и инициализируем экран
    ld a, $91  ; включение LCD, BG и окон
    ld [$FF40], a

    ; Ожидание стабилизации экрана
    call WaitVBlank

    ; Очистка экрана
    call ClearScreen

    ; Загрузка данных символов в VRAM
    ld hl, CANFLY_TILES
    ld de, $8000
    ld bc, 48  ; 6 символов по 8 байт
LoadTilesLoop:
    ld a, [hl+]
    ld [de], a
    inc de
    dec bc
    ld a, b
    or c
    jr nz, LoadTilesLoop

    ; Размещение текста "CANFLY" на экране
    ld hl, $9800           ; Адрес Tile Map
    ld [hl], $00           ; 'C'
    inc hl
    ld [hl], $01           ; 'A'
    inc hl
    ld [hl], $02           ; 'N'
    inc hl
    ld [hl], $03           ; 'F'
    inc hl
    ld [hl], $04           ; 'L'
    inc hl
    ld [hl], $05           ; 'Y'

MainLoop:
    jp MainLoop

WaitVBlank:
    ld a, $01
    ld [$FF0F], a
WaitLoop:
    ld a, [$FF0F]
    bit 0, a
    jr nz, WaitLoop
    ret

ClearScreen:
    ld hl, $9800
    ld bc, 32 * 32        ; 32x32 Tile Map
    xor a
ClearLoop:
    ld [hl+], a
    dec bc
    ld a, b
    or c
    jr nz, ClearLoop
    ret
