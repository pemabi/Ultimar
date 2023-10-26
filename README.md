# Ultimar
Ultimar chess variant with basic AI. Made for TG.

Project used as an introduction to Python and Git.

Massive thanks to Eddie Sharick https://www.youtube.com/@eddiesharick6649 and his series of youtube videos on building a chess engine with python/pygame - was my introduction to learning python and serves as the foundation for much of this code (easy to tell whose is whose!).

Credit also to the V&A South Kensington for the use of their tile graphic https://www.vam.ac.uk/articles/design-and-make-your-own-islamic-tile-and-printed-pattern

recommended depth: 2/3

The Rules of Ultimar (as writted by TG)

Objective
To take the opponents King.
Starting board layout
As for chess board but:
1. White Queen is swapped with White King (White King is on its own
colour).
2. Left hand Rook is inverted (turned upside down).
The Piece names (running left to right)
Pawn = Pawn
Immobiliser = Inverted Rook
Long Leaper = Knight
Chameleon = Bishop
King = King
Withdrawer = Queen
Co-ordinator = Rook
How the Pieces Move
1. The King moves like a chess King.
2. The Pawns move like chess Rooks.
3. All other pieces move like a chess Queen.

How the Pieces Act
King
Takes other pieces in the same manner as a chess King.
Pawn
A Pawn takes by moving alongside an opponents piece which
has one of the attackers piece on its other side. Pawns only
take along the rank and file not on diagonals.
Immobiliser
An Immobiliser is not able to take opponents pieces. However
what it can do is immobilise all opponents pieces on immediately
adjoining squares. In this manner an Immobiliser could
theoretically Immobilise up to seven pieces at a time.
Opponents pieces moving alongside an Immobiliser are not
immobilised (the Immobiliser must move up to the opponents
pieces to affect an immobilisation).
Long Leaper
The Long Leaper takes by jumping over one or more opponents
pieces (rank, file or diagonal. The Long Leaper does not have
to be alongside the opponents pieces in order to take them.
The Long Leaper is not able to jump over two occupied squares
at a time (there must be at least one square to land on between
each piece taken). In this manner a Long Leaper could
theoretically take up to three opponents pieces at a time. A
Long Leaper may not jump over any of its own pieces.

Withdrawer
The Withdrawer takes by moving up to a Piece on one move an
moving away on a subsequent move. When a piece is taken,
all adjoining opponents pieces on the line of withdrawal are also
taken. In this manner a Withdrawer could theoretically take up to
six opponents pieces at a time. If an opponent’s piece moves
up to a Withdrawer the Withdrawer would not take it on
withdrawal (the Withdrawer would have to move to another
adjoining square first and then withdraw).
Co-ordinator
A Co-ordinator takes pieces on the square(s) which are on a
rank/file line between the King and the Co-ordinator. The King
cannot take in this manner, it is the movement of the Co-
ordinator which initiates the take. The Intervening squares on
the co-ordination paths do not have to be empty. In this manner
a Co-ordinator could theoretically take up to two opponents
pieces at a time (although one at a time is the norm).

Chameleon
This is the most complex piece to describe.
A Chameleon imitates the pieces it is acting on. Therefore it is
best to describe the Chameleon in terms of the pieces it
interacts with (each piece may only be taken in the manner in
which it takes itself):
King
The Chameleon may take a King in the manner of a King
taking another piece, i.e. moving ONLY one square in
any possible direction onto the piece is question.
Pawn
The Chameleon may take a Pawn as a Pawn takes any
other piece. The Chameleon MUST move as a Pawn i.e.
in rank and file to take a Pawn.
Immobiliser
The Chameleon is not able to take an Immobiliser.
However if a Chameleon moves alongside an Immobiliser
then all the opponents pieces surrounding the
Chameleon (including the Immobiliser itself) are
Immobilised. This does not Un-immobilise any pieces
that were previously Immobilised by the opponents
Immobiliser. The Chameleon is effectively an
Immobiliser itself while in this position. (If the opponents
adjoining Immobiliser is subsequently taken then the
Chameleon is no longer Immobilising the pieces in
question).
Long Leaper
A Chameleon may take a Long Leaper in the manner of a
Long Leaper. It should be noted that to take two pieces
simultaneously in this manner would necessitate both the
opponents pieces being Long Leapers. The Chameleon
is only a Long Leaper when taking a Long Leaper.
Withdrawer
A Chameleon may move up to a Withdrawer and take the
Withdrawer and any pieces in line in the manner of the
Withdrawer.

Co-ordinator
A Chameleon may take a Co-ordinator if the opponents
piece is sitting on the square which becomes the rank/file
co-ordination point between the Chameleon and its own
King.
Chameleon
A Chameleon may not do much with an opponent’s
Chameleon except when the opponents Chameleon is
Immobilising an Immobiliser. In this case the attackers
Chameleon also takes on Immobilising features.
Combinations
Simultaneous combinations of all the above are possible
providing each individual criteria is observed.

UNCLEAR if the withdrawer moves but still stays in
contact with the Chameleon whether the Cameleon can
still take the withdrawerer, this can be simplified by the
question of: I withdrawer moves up to any piece, if that
pieces stays in contact but moves around the withdrawer,
can the withdrawer still take it? We played rules that
said any contact maintained means the chameleon did
not have to withdraw and re-withdraw