zip -r ../AgoBot.zip *
echo '#!/usr/bin/env python3' | cat - ../AgoBot.zip > AgoBot
chmod +x AgoBot
nohup ./AgoBot $1 &
