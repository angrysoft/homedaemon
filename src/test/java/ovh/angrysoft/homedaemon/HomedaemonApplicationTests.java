package ovh.angrysoft.homedaemon;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

@SpringBootTest(classes = HomedaemonApplicationTests.class)
class HomedaemonApplicationTests {
    ApplicationModules modules = ApplicationModules.of(HomedaemonApplication.class);

	@Test
	void contextLoads() {
	}

    @Test
    void verifyTest() {
        modules.verify();
    }

    @Test
    void printModules() {
        modules.forEach(System.out::println);
    }

    @Test
    void writeDocumentationSnippets() {

        new Documenter(modules).writeModulesAsPlantUml().writeIndividualModulesAsPlantUml()
                .writeAggregatingDocument();
    }

}
