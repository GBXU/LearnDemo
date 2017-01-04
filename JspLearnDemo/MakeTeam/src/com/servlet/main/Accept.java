package com.servlet.main;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.PreparedStatement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.mysql.jdbc.Connection;
import com.servlet.bean.UserBean;
import com.servlet.util.Dbutil;

/**
 * Servlet implementation class Accept
 */
@WebServlet("/Accept")
public class Accept extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Accept() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String projectid = request.getParameter("projectid");
		HttpSession session = request.getSession(true);
		String applicant = request.getParameter("applicant");
		UserBean user = (UserBean)session.getAttribute("user");
		if(user==null){
			getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
		}
        try {  
            Connection con=(Connection) Dbutil.getConnection();  
            String sql="insert into member(projectid,userid) values(?,?)";
            PreparedStatement stmt=con.prepareStatement(sql);
            stmt.setInt(1, Integer.valueOf(projectid));
            stmt.setInt(2,Integer.valueOf(applicant));
            int rs=stmt.executeUpdate();
            
            String sql1="delete from application where projectid=? and userid=? ";
            PreparedStatement stmt1=con.prepareStatement(sql1);
            stmt1.setInt(1, Integer.valueOf(projectid));
            stmt1.setInt(2,Integer.valueOf(applicant));
            int rs1=stmt1.executeUpdate();
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
