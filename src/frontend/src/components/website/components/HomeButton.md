# HomeButton

Ein wiederverwendbarer Button mit konfigurierbarem Typ, Stil (Farbe, Größe) und deaktivierbarem Zustand. <HomeButton color="secondary" size="large" @click="handleClick">Klick mich</HomeButton>

## Props

<!-- @vuese:HomeButton:props:start -->
|Name|Description|Type|Required|Default|
|---|---|---|---|---|
|type|Der Typ des Buttons (z. B. "button", "submit", "reset")|`String`|`false`|button|
|color|Die Farbklasse des Buttons, z. B. "primary" oder "secondary"|`String`|`false`|primary|
|size|Die Größenklasse des Buttons, z. B. "normal" oder "large"|`String`|`false`|normal|
|disabled|Ob der Button deaktiviert ist|`Boolean`|`false`|false|

<!-- @vuese:HomeButton:props:end -->


## Events

<!-- @vuese:HomeButton:events:start -->
|Event Name|Description|Parameters|
|---|---|---|
|click|-|-|

<!-- @vuese:HomeButton:events:end -->


## Slots

<!-- @vuese:HomeButton:slots:start -->
|Name|Description|Default Slot Content|
|---|---|---|
|default|-|-|

<!-- @vuese:HomeButton:slots:end -->


