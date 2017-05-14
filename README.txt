# golddigger

Instructions:
Main Game:
	How to play:
		Find your way to the exit

	Controls:
		" w ": Jump
		" a ": Left
		" s ": Down
		" d ": Right
		" h ": Health Plus (cheatB)

	Objects:
		" -o- " Player (Moves with w, a, s, d)
		" ~o~ " Player (Falling)
		" ▒▒▒ " Dirt. (health 2/2 - Player can dig through dirt to make tunnels)
		" ░░░ " Dirt. (health 1/2)
		" [#] " Stone. (Stone can fall and hurt any character and only certain objects)
		" [$] " Gold. (health 3/3 - Player can break gold blocks to get a gold pickup)
		" ($) " Gold. (health 2/3)
		" {$} " Gold. (health 1/3)
		"  $  " Gold Pickup. (Increases players gold by one)
		"  +  "  Health Pickup (Increases players health by one)
		" ███ " Wall (Impenetrable object that can block explosions)
		" ▓▓▓ " Smoke (Created when bomb explodes)
		" ö>> " Enemy (Moving right)
		" <<ö " Enemy (Moving left)
		" Ö»» " Enemy (Moving right - can dig and damage bomb blocks)
		" ««Ö " Enemy (Moving left - can dig and damage bomb blocks)
		" Ö═╣ " Enemy (Moving right - can push certain objects)
		" ╠═Ö " Enemy (Moving left - can push certain objects)	
		" [3] " Bomb (health 2/2 - Will fall when damaged and explode after the fuse is lit, number displays fuse time)
		" [!] " Bomb (health 1/2 - Can fall and damage any character)
		" [3] [2] [1]" Bomb (health 0/2 - Counts down from three then explodes)


Level Editor:
	How to play:
		Move around and place blocks to make your own custom level.

	Controls:
		" w ": Jump
		" a ": Left
		" s ": Down
		" d ": Right
		" 0 ": Deletes the object selected
		" 1 ": Places a Wall block
		" 2 ": Places a Dirt block
		" 3 ": Places a Stone block
		" 4 ": Places a Gold block
		" 5 ": Places a Gold pickup
		" 6 ": Places a Health pickup
		" 7 ": Places a Player spawn block
		" 8 ": Places a Door block
		" 9 ": Places an Enemy
		" . ": Places a Bomb block
		" - ": Decreases health of certain objects
		" + ": Increases health of certain objects
		" / ": Switches Enemy's direction, decreases Bomb fuse time
		" * ": Switches Enemy's canDig and canPush bool, increases Bomb fuse time
		Spacebar: Places a marker to make it easier to fill in a large aria with objects
		ENTER: Explodes Bombs	

	Objects:
		" {   " Editor Cursor (Moves with w, a, s, d and can place objects with numbers)
		"  *  " Editor Marker (If there is a marker on the map, you will be able to fill
			in the whole aria between the marker and the cursor)
		" [P] " Player Spawn block (This is where the player will spawn)
		" [D] " Door block (Exit for the level)
