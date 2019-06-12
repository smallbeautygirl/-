
import java.util.ArrayList;
import java.util.Formatter;
import java.util.Scanner;
import java.util.Vector;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import javax.swing.JFrame;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

import java.awt.Font;
import java.awt.BorderLayout;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.*;

public class server {
  private int port;// server port
  private Vector<Client> clients;
  public Vector<Database> databases;// store client's account and password
  public Vector<Socket> cli_socket;
  private Socket socket = null;
  private ServerSocket serverSocket;
  private playclass play;
  private boolean one ;
  //private int countplayer;

  public static void main(String[] args) {
    try {
      if (args.length != 1) {
        System.out.println("Usage: java Server [port]");
        return;
      }
      server ser = new server(Integer.parseInt(args[0]));
      ser.listen();
    } catch (Exception e) {
      System.out.println(e);
    }
  }

  public server(int port) {
    this.port = port;
    this.clients = new Vector<Client>();
    this.databases = new Vector<Database>();
    this.play = new playclass();
    this.one = true;
    //this.countplayer = 1;
    // 內建的資料
    Database d1 = new Database();
    d1.setAccount("11111");
    d1.setPassword("11111");
    Database d2 = new Database();
    d2.setAccount("22222");
    d2.setPassword("22222");
    Database d3 = new Database();
    d3.setAccount("33333");
    d3.setPassword("33333");
    this.databases.add(d1);
    this.databases.add(d2);
    this.databases.add(d3);
  }

  public void listen() {
    try {
      this.serverSocket = new ServerSocket(this.port);
      System.out.println("Server listening on port " + this.port);

      while (true) {
        this.socket = serverSocket.accept();
        System.out.println("Client connection success!!");
        Client client = new Client(socket);
        this.clients.add(client);

        client.start();
      }
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      try {
        if (serverSocket != null)
          this.serverSocket.close();
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
  }

  // 進入waiting room (傳正在waiting的玩家給client讓他顯示)
  public void broadcast() {
    System.out.println("broadcast");
    System.out.println(databases.size());
    try {
      for (int j = 0; j < clients.size(); ++j) {
        if (clients.get(j).getState() != Thread.State.TERMINATED) {
          for (int i = 0; i < databases.size(); ++i) {
            System.out.println(i);
            if (databases.get(i).getState().equals("wait")) {
              clients.get(j).sendData(databases.get(i).getAccount());
              System.out.println(databases.get(i).getAccount());
              clients.get(j).sendData(Integer.toString(databases.get(i).getWin()));
              System.out.println(Integer.toString(databases.get(i).getWin()));
              clients.get(j).sendData(Integer.toString(databases.get(i).getLose()));
              System.out.println(Integer.toString(databases.get(i).getLose()));
            }
          }
        } else
          clients.remove(j);
      }
    } catch (IOException e1) {
      // TODO Auto-generated catch block
      e1.printStackTrace();
    }
  }

  public boolean checkAccountExist(String account, String password) {
    for (int i = 0; i < this.databases.size(); ++i) {
      if (this.databases.get(i).getAccount().equals(account) && this.databases.get(i).getPassword().equals(password)) {
        return true;
      }
    }
    return false;
  }

  public int countWaitNum() {
    int count = 0;
    for (int i = 0; i < this.databases.size(); ++i) {
      if (this.databases.get(i).getState().equals("wait")) {
        count++;
      }
    }
    return count;
  }

  class Client extends Thread {
    private Socket clientSocket = null;// client 的 socket
    private DataInputStream dataInputStream;
    private DataOutputStream dataOutputStream;

    public Client(Socket clientSocket) {
      this.clientSocket = clientSocket;
    }

    public void run() {
      try {
        this.getStreams();
        System.out.println("run");

        while (true) {
          String action = null;// mainframe 的動作(sign in , create,exit)
          String account = null;
          String password = null;
          boolean AccountIsExist = false;
          action = dataInputStream.readUTF();
          if (action.equals("sign in")) {// 若是sign in則檢查這個帳號密碼是否存在
            account = dataInputStream.readUTF();
            password = dataInputStream.readUTF();
            AccountIsExist = checkAccountExist(account, password);
            // 若這個帳戶存在就傳true然後把state改為wait，不存在就傳false
            if (AccountIsExist) {
              this.sendData("true");
              for (int i = 0; i < databases.size(); ++i) {
                if (databases.get(i).getAccount().equals(account)) {
                  databases.get(i).setState("wait");
                  databases.get(i).setSocket(this.clientSocket);
                  break;
                }
              }

              break;
            } else {
              this.sendData("false");
            }
          } else if (action.equals("create")) {
            account = dataInputStream.readUTF();
            password = dataInputStream.readUTF();
            System.out.println("account:" + account + " password:" + password);
            AccountIsExist = checkAccountExist(account, password);
            // 若這個帳戶存在就傳true，不存在就傳false然後把新增的帳戶放入databases vector裡並且把他的狀態設為wait
            if (AccountIsExist) {
              this.sendData("true");
              System.out.println("send");
            } else {
              this.sendData("false");
              Database database = new Database();
              database.setAccount(account);
              database.setPassword(password);
              database.setState("wait");
              database.setSocket(this.clientSocket);
              databases.add(database);
              // System.out.println(databases.get(3).getAccount()+"
              // "+databases.get(3).getPassword()+" "+databases.get(3).getState());
              break;
            }
          } else if (action.equals("exit")) {
            break;
          }
        }
        broadcast();
        String start = null;
        String name = null;
        Socket player = null;
        

        name = dataInputStream.readUTF();
        //if(one){
          sendData("end");
          //one = false;
        //}
        start = dataInputStream.readUTF();
        if (start.equals("start")) {
          // playclass play = new playclass();
          for (int i = 0; i < databases.size(); ++i) {
            if (databases.get(i).getAccount().equals(name)) {
                player = databases.get(i).getSocket();
                break;
            }
          }
          play.checkIftwoPlayer(player,name);
          
        }
        // while(true){}
      } catch (IOException e1) {
        // TODO Auto-generated catch block
        e1.printStackTrace();
      }
    }

    public void getStreams() throws IOException {
      this.dataInputStream = new DataInputStream(socket.getInputStream());
      this.dataOutputStream = new DataOutputStream(socket.getOutputStream());
    }

    public void sendData(String message) throws IOException {
      this.dataOutputStream.writeUTF(message);
    }
  }

  class playclass extends Thread{
    private JTextArea outputArea;// for outputting moves
    private ExecutorService runGame;
    private Lock gameLock;// to lock game for synchronization
    private Condition otherPlayerTurn;
    private Condition otherPlayerConnected;
    private String[] board = new String[9];// tic-tac-toe board
    private Player[] players;// array of players
    private int currentPlayer; // keep track of player with current move
    private final static int PLAYER_X = 0;
    private final static int PLAYER_O = 1;
    private String[] MARKS = { "X", "O" };

    private int checkTwoPlayer;
    private Socket player1Socket=null;
    private Socket player2Socket=null;
    private String name1=null;
    private String name2=null;

    public playclass() {
      System.out.println("playclass contructor");
      this.checkTwoPlayer = 1;
      runGame = Executors.newFixedThreadPool(2);
      gameLock = new ReentrantLock();// create lock for game

      // condition variable for the other player's turn
      otherPlayerTurn = gameLock.newCondition();
      otherPlayerConnected = gameLock.newCondition();

      for (int i = 0; i < 9; ++i) {
        board[i] = new String("");
      }
      players = new Player[2];
      currentPlayer = PLAYER_X;// set current player to first player

      startTicTacToe st = new startTicTacToe();
    }
    public void checkIftwoPlayer(Socket socket,String name){
        System.out.println(this.checkTwoPlayer);
        if(this.checkTwoPlayer==1){
          this.checkTwoPlayer++;
          this.player1Socket = socket;
          this.name1 = name;
        }else{
            this.player2Socket = socket;
            this.name2 = name;
            execute(this.player1Socket, this.player2Socket,this.name1,this.name2);
        }
    }
    public void execute(Socket socket1,Socket socket2,String name1,String name2) {
      System.out.println("execute");
      //for (int i = 0; i < players.length; ++i) {
        players[0] = new Player(socket1, 0,name1);
        runGame.execute(players[0]);
        players[1] = new Player(socket2, 1,name2);
        runGame.execute(players[1]);
     // }
      gameLock.lock();

      try {
        players[PLAYER_X].setSuspended(false);
        otherPlayerConnected.signal();
      } finally {
        gameLock.unlock();
      }
    }

    private void displayMessage(final String messageToDisplay) {
      SwingUtilities.invokeLater(new Runnable() {
        public void run() {
          outputArea.append(messageToDisplay);// update output
        }
      });
    }

    public boolean validateAndMove(int location, int player) {
      // while not current player, must wait for turn
      while (player != currentPlayer) {
        gameLock.lock();// lock game to wait for other player to go

        try {
          otherPlayerTurn.await();// wait for player's turn
        } catch (InterruptedException e) {
          e.printStackTrace();
        } finally {
          gameLock.unlock();
        }
      }
      if (!isOccupied(location)) {
        board[location] = MARKS[currentPlayer];// set move on board

        currentPlayer = (currentPlayer + 1) % 2;// change player

        // let new current player know that move occurred
        players[currentPlayer].otherPlayerMoved(location);

        gameLock.lock();// lock game to signal other player to go

        try {
          otherPlayerTurn.signal();// signal other player to continue
        } finally {
          gameLock.unlock();
        }
        return true;
      } else {
        return false;
      }
    }

    // determine whether location is occupied
    public boolean isOccupied(int location) {
      if (board[location].equals(MARKS[PLAYER_X]) || board[location].equals(MARKS[PLAYER_O])) {
        return true;
      } else {
        return false;
      }
    }

    public boolean isGameOver() {
      return false;
    }

    class startTicTacToe extends JFrame {
      public startTicTacToe() {
        super("Tic-Tac-Toe Information");
        outputArea = new JTextArea();
        add(outputArea, BorderLayout.CENTER);
        outputArea.setText("waiting...\n");
        outputArea.setFont(new Font("Arial", 0, 30));
        setSize(600, 600);
        setVisible(true);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      }

    }

    class Player implements Runnable {
      private String name=null;
      private Scanner input=null;
      private Formatter output=null;
      private Socket connection=null;
      private int playerNumber=0;
      private String mark;
      private boolean suspended = true;// whether thread is suspend
      private ArrayList storeLocation;
      public Player(Socket socket, int number,String name) {
        System.out.println("player constructor");
        this.playerNumber = number;
        this.mark = MARKS[this.playerNumber];
        this.connection = socket;
        this.input = null;
        this.output = null;
        this.name = name;
        this.storeLocation = new ArrayList<>();
      }
      public void getStreams(){
        try {
          this.input = new Scanner(this.connection.getInputStream());
          this.output = new Formatter(this.connection.getOutputStream());
        } catch (IOException e) {
          e.printStackTrace();
        }
      }
      // send message that other player moved
      public void otherPlayerMoved(int location) {
        output.format("Opponent moved\n");
        output.format("%d\n", location);
        output.flush();
      }

      public void run() {
        System.out.println("run player "+this.mark);
        this.getStreams();

        // send client its mark(X or O),process message from client
        try {
          displayMessage("Player" + this.name + " play("+mark+")\n");
          output.format("%s\n", this.mark);
          output.flush();

          // if playerX ,wait for another player to arrive
          if (playerNumber == PLAYER_X) {
            output.format("%s%s", "Player X connected\n","waiting for another players\n");
            output.flush();

            gameLock.lock();// lock game to wait for second player

            try {
              while (suspended) {
                otherPlayerConnected.await();// wait for player O
              }
            } catch (Exception e) {
              // TODO: handle exception
              e.printStackTrace();
            } finally {
              gameLock.unlock();// unlock game after second player
            }

            // send message that other player connected
            output.format("Other player connected. Your move\n");
            output.flush();
          } else {
            output.format("Player O connected, please wait\n");
            output.flush();
          }

          // while game not over
          while (!isGameOver()) {
            int location = 0;// initialize move location
    
            if(this.storeLocation.contains(0)&&this.storeLocation.contains(1)&&this.storeLocation.contains(2)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
              break;
            }else if(this.storeLocation.contains(3)&&this.storeLocation.contains(4)&&this.storeLocation.contains(5)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(6)&&this.storeLocation.contains(7)&&this.storeLocation.contains(8)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(0)&&this.storeLocation.contains(3)&&this.storeLocation.contains(6)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(1)&&this.storeLocation.contains(4)&&this.storeLocation.contains(7)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(2)&&this.storeLocation.contains(5)&&this.storeLocation.contains(8)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(0)&&this.storeLocation.contains(4)&&this.storeLocation.contains(8)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }else if(this.storeLocation.contains(2)&&this.storeLocation.contains(4)&&this.storeLocation.contains(6)){
              displayMessage("\n"+this.name+" win!!\n");
              output.format(this.name+" win!!\n");
              output.flush();
            }
            if (input.hasNext()) {
              location = input.nextInt();// get move location
            }

            if (validateAndMove(location, playerNumber)) {
              displayMessage("\nlocation: " + location);
              output.format("Valid move\n");
              output.flush();
              this.storeLocation.add(location);
            } else {
              output.format("InValid move, try again\n");
              output.flush();
            }
          }
        } finally {
          try {
            connection.close();
          } catch (IOException e) {
            e.printStackTrace();
          }
        }
      }

      public void setSuspended(boolean status) {
        suspended = status;
      }
    }
  }

  class Database {
    private String cli_account = null;
    private String cli_password = null;
    private int win;// 勝場數
    private int lose;// 敗場數
    private String cli_state = null;// client狀態(wait, play)
    private Socket cli_socket = null;

    public Database() {
      this.cli_account = "none";
      this.cli_password = "none";
      this.win = 0;
      this.lose = 0;
      this.cli_state = "offline";
    }

    public void setAccount(String account) {
      this.cli_account = account;
    }

    public void setPassword(String password) {
      this.cli_password = password;
    }

    public void setState(String state) {
      this.cli_state = state;
    }

    public void setWin(int win) {
      this.win = win;
    }

    public void setLose(int lose) {
      this.lose = lose;
    }

    public void setSocket(Socket socket) {
      this.cli_socket = socket;
    }

    public String getAccount() {
      return this.cli_account;
    }

    public String getPassword() {
      return this.cli_password;
    }

    public String getState() {
      return this.cli_state;
    }

    public int getWin() {
      return this.win;
    }

    public int getLose() {
      return this.lose;
    }

    public Socket getSocket() {
      return this.cli_socket;
    }
  }
}