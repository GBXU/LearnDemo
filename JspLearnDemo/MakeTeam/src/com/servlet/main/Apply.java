package com.servlet.main;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;
import com.servlet.bean.UserBean;
import com.servlet.util.Dbutil;

/**
 * Servlet implementation class Apply
 */
@WebServlet("/Apply")
public class Apply extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Apply() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

    }

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String projectid = request.getParameter("projectid");
		HttpSession session = request.getSession(true);
		UserBean user = (UserBean)session.getAttribute("user");
		if(user==null){
			getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
		}
        try {  
            Connection con=(Connection) Dbutil.getConnection();  
            String sql="insert into application(projectid,userid) values(?,?)";
            PreparedStatement stmt=con.prepareStatement(sql);
            stmt.setInt(1, Integer.valueOf(projectid));
            stmt.setInt(2,user.getUserId());
            int rs=stmt.executeUpdate();  
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
        String tmp = "/projectdetail.jsp?projectid="+projectid;
        getServletContext().getRequestDispatcher(tmp).forward(request, response);
	}

}
