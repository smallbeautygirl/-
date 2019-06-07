import java.io.*;

public class Info implements Serializable {
	public String name	= null;
	public String state	= null;

	Info(String name, String state) {
		this.name	= name;
		this.state	= state;
	}
}
