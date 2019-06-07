
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Vector;
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
  private Socket socket = null;
  private ServerSocket serverSocket;
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
        // this.broadcast();

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

  public void broadcast() {

  }

  public boolean checkAccountExist(String account, String password) {
    for (int i = 0; i < this.databases.size(); ++i) {
      if (this.databases.get(i).getAccount().equals(account) && this.databases.get(i).getPassword().equals(password)) {
        return true;
      }
    }
    return false;
  }

  public int countWaitNum(){
    int count=0;
    for(int i=0;i<this.databases.size();++i){
      if(this.databases.get(i).getState().equals("wait")){
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
            System.out.println("account:"+account+" password:"+password);
            AccountIsExist = checkAccountExist(account, password);
            //若這個帳戶存在就傳true，不存在就傳false然後把新增的帳戶放入databases vector裡並且把他的狀態設為wait
            if (AccountIsExist) {
              this.sendData("true");
              System.out.println("send");
            } else {
              this.sendData("false");
              Database database = new Database();
              database.setAccount(account);
              database.setPassword(password);
              database.setState("wait");
              databases.add(database);
              //System.out.println(databases.get(3).getAccount()+"  "+databases.get(3).getPassword()+" "+databases.get(3).getState());
              break;
            }
          } else if (action.equals("exit")) {
              break;
          }
       }
       //進入waiting room (傳正在waiting的玩家給client讓他顯示)
       int countwait=0;//幾位玩家在等
       countwait = countWaitNum();
       this.sendData(Integer.toString(countwait));//先傳幾個人在wait
       for(int i=0;i<databases.size();++i){
         if(databases.get(i).getState().equals("wait")){
            this.sendData(databases.get(i).getAccount());
            this.sendData(Integer.toString(databases.get(i).getWin()));
            this.sendData(Integer.toString(databases.get(i).getLose()));
         }
       }
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

  class Database {
    private String cli_account = null;
    private String cli_password = null;
    private int win;// 勝場數
    private int lose;// 敗場數
    private String cli_state = null;// client狀態(wait, play)

    public Database() {
      this.win = 0;
      this.lose = 0;
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
    public void setWin(int win){
      this.win = win;
    }
    public void setLose(int lose){
      this.lose = lose;
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
    public int getWin(){
      return this.win;
    }
    public int getLose(){
      return this.lose;
    }
  }
}